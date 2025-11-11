from django.contrib import admin
from django.utils.html import format_html
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['languages_needed', 'job_type', 'date', 'time', 'full_address', 'assigned_interpreter', 'status', 'payment', 'mileage_included', 'requires_dshs_certification', 'created_at']
    list_filter = ['status', 'job_type', 'date', 'state', 'requires_dshs_certification', 'mileage_included', 'assigned_interpreter', 'spanish', 'russian', 'portuguese', 'mandarin', 'somali', 'farsi', 'vietnamese', 'amharic', 'tigrinya']
    search_fields = ['street_address', 'city', 'state', 'zip_code', 'assigned_interpreter__first_name', 'assigned_interpreter__last_name']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']

    readonly_fields = ['available_interpreters_display']

    fieldsets = (
        ('Job Details', {
            'fields': ('job_type', 'date', 'time', 'status')
        }),
        ('Location', {
            'fields': ('street_address', 'city', 'state', 'zip_code')
        }),
        ('Languages Needed', {
            'fields': ('amharic', 'farsi', 'mandarin', 'portuguese', 'russian', 'somali', 'spanish', 'tigrinya', 'vietnamese'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('payment', 'mileage_included')
        }),
        ('Requirements', {
            'fields': ('requires_dshs_certification',)
        }),
        ('Request Interpreter', {
            'fields': ('assigned_interpreter', 'available_interpreters_display'),
            'description': 'Assign an interpreter to this job'
        }),
    )

    def full_address(self, obj):
        """Display full address in the list view"""
        return f"{obj.street_address}, {obj.city}, {obj.state} {obj.zip_code}"
    full_address.short_description = 'Location'

    def languages_needed(self, obj):
        """Display languages needed in the list view"""
        languages = obj.get_languages()
        return ', '.join(languages) if languages else 'None'
    languages_needed.short_description = 'Languages'

    def available_interpreters_display(self, obj):
        """Display available interpreters who match this job's requirements"""
        if not obj.id:
            return '-'

        from accounts.models import InterpreterProfile

        # Get job's required languages
        job_languages = set(obj.get_languages())

        if not job_languages:
            return 'No languages specified for this job'

        # Start with all interpreters
        interpreters = InterpreterProfile.objects.all()

        # Filter by DSHS certification if required
        if obj.requires_dshs_certification:
            interpreters = interpreters.filter(dshs_certified=True)

        # Find interpreters who speak required languages
        # NOTE: Distance filtering temporarily disabled for performance
        matching_interpreters = []
        for interpreter in interpreters:
            interpreter_languages = set(interpreter.get_languages())

            # Check if interpreter speaks any of the required languages
            if job_languages.intersection(interpreter_languages):
                matching_languages = job_languages.intersection(interpreter_languages)
                matching_interpreters.append({
                    'interpreter': interpreter,
                    'languages': matching_languages,
                    'distance': 0  # Distance calculation disabled temporarily
                })

        if not matching_interpreters:
            return 'No matching interpreters found'

        # Sort by interpreter name
        matching_interpreters.sort(key=lambda x: (x['interpreter'].last_name, x['interpreter'].first_name))

        # Generate sample message
        languages_str = ', '.join(sorted(job_languages))
        sample_message = f"""Hello,

We have a new interpretation job available that matches your qualifications:

Job Type: {obj.get_job_type_display()}
Languages Needed: {languages_str}
Date: {obj.date.strftime('%B %d, %Y')}
Time: {obj.time.strftime('%I:%M %p')}
Location: {obj.street_address}, {obj.city}, {obj.state} {obj.zip_code}
Payment: ${obj.payment}
{"Mileage: Included" if obj.mileage_included else ""}
{"DSHS Certification Required" if obj.requires_dshs_certification else ""}

Please respond YES to accept this job. In the event that you need to cancel, YOU MUST CALL THE AGENCY DIRECTLY. CANCELLATIONS ARE NOT ACCEPTED VIA TEXT.

Thank you!"""

        # Format as HTML with checkboxes
        html = '<div style="margin-top: 10px;" id="interpreter-selector">'
        html += f'<p style="margin-bottom: 8px; font-weight: bold;">Found {len(matching_interpreters)} matching interpreter(s):</p>'

        # Select All checkbox
        html += '<div style="margin-bottom: 10px; padding: 10px; background-color: #f3f4f6; border-radius: 4px;">'
        html += '<label style="cursor: pointer;"><input type="checkbox" id="select-all-interpreters" style="margin-right: 8px;"> <strong>Select All</strong></label>'
        html += '</div>'

        # Interpreter list with checkboxes
        html += '<div style="max-height: 400px; overflow-y: auto; border: 1px solid #e5e7eb; border-radius: 4px; padding: 10px;">'

        for item in matching_interpreters[:15]:  # Limit to 15
            interp = item['interpreter']
            langs = ', '.join(sorted(item['languages']))

            html += f'<div style="margin-bottom: 8px; padding: 8px; border-bottom: 1px solid #e5e7eb;">'
            html += f'<label style="cursor: pointer; display: flex; align-items: center;">'
            html += f'<input type="checkbox" class="interpreter-checkbox" '
            html += f'data-name="{interp.first_name} {interp.last_name}" '
            html += f'data-email="{interp.email_address}" '
            html += f'data-phone="{interp.phone_number}" '
            html += f'style="margin-right: 8px;">'
            html += f'<span><strong>{interp.first_name} {interp.last_name}</strong> - {langs}'
            if interp.dshs_certified:
                html += ' <span style="color: #059669; font-weight: bold;">(DSHS)</span>'
            html += f' - {interp.city}, {interp.state}'
            html += f'<br><span style="color: #6B7280; font-size: 0.9em;">📧 {interp.email_address} | 📞 {interp.phone_number}</span>'
            html += '</span></label></div>'

        if len(matching_interpreters) > 15:
            html += f'<div style="color: #666; padding: 8px;">...and {len(matching_interpreters) - 15} more</div>'

        html += '</div>'

        # Send Message button
        # Escape the message for JavaScript
        js_message = sample_message.replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")

        html += '<div style="margin-top: 15px;">'
        html += f'<button type="button" id="send-message-btn" onclick="openMessageDialog(\'{js_message}\', {obj.id})" '
        html += 'style="background-color: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">'
        html += 'Send Message</button>'
        html += '<span id="selected-count" style="margin-left: 15px; color: #6B7280;">0 interpreters selected</span>'
        html += '</div>'

        html += '</div>'

        # JavaScript for checkbox functionality and message dialog
        html += '''
        <script>
        (function() {
            // Use setTimeout to ensure elements are rendered
            setTimeout(function() {
                const selectAll = document.getElementById('select-all-interpreters');
                const checkboxes = document.querySelectorAll('.interpreter-checkbox');
                const selectedCount = document.getElementById('selected-count');

                console.log('Initializing interpreter selector');
                console.log('Select All:', selectAll);
                console.log('Checkboxes found:', checkboxes.length);
                console.log('Selected Count:', selectedCount);

                if (!selectAll || !selectedCount) {
                    console.error('Required elements not found');
                    return;
                }

                function updateCount() {
                    const count = document.querySelectorAll('.interpreter-checkbox:checked').length;
                    console.log('Updating count:', count);
                    selectedCount.textContent = count + ' interpreter' + (count !== 1 ? 's' : '') + ' selected';
                }

                selectAll.addEventListener('change', function() {
                    console.log('Select all changed:', this.checked);
                    checkboxes.forEach(cb => cb.checked = this.checked);
                    updateCount();
                });

                checkboxes.forEach(cb => {
                    cb.addEventListener('change', function() {
                        console.log('Checkbox changed');
                        selectAll.checked = Array.from(checkboxes).every(cb => cb.checked);
                        updateCount();
                    });
                });

                // Initial count update
                updateCount();
            }, 100);

            window.openMessageDialog = function(sampleMessage, jobId) {
                const selected = Array.from(document.querySelectorAll('.interpreter-checkbox:checked'));

                if (selected.length === 0) {
                    alert('Please select at least one interpreter to send a message.');
                    return;
                }

                const interpreterList = selected.map(cb =>
                    cb.dataset.name + ' (' + cb.dataset.email + ')'
                ).join('\\n');

                const dialog = document.createElement('div');
                dialog.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; align-items: center; justify-content: center;';
                dialog.setAttribute('data-job-id', jobId);

                const formattedList = interpreterList.replace(/\\n/g, '<br>');

                dialog.innerHTML =
                    '<div style="background: white; padding: 30px; border-radius: 8px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;">' +
                        '<h2 style="margin-top: 0; color: #1f2937;">Send Message to Interpreters</h2>' +
                        '<p style="color: #6B7280; margin-bottom: 15px;">Sending to ' + selected.length + ' interpreter(s):</p>' +
                        '<div style="background: #f3f4f6; padding: 10px; border-radius: 4px; margin-bottom: 20px; max-height: 100px; overflow-y: auto; font-size: 0.9em;">' +
                            formattedList +
                        '</div>' +
                        '<label style="display: block; margin-bottom: 8px; font-weight: bold; color: #374151;">Message:</label>' +
                        '<textarea id="message-text" rows="12" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 4px; font-family: sans-serif; font-size: 14px;">' + sampleMessage + '</textarea>' +
                        '<div style="margin-top: 20px; display: flex; gap: 10px; justify-content: flex-end;">' +
                            '<button onclick="this.closest(\\'div\\').parentElement.parentElement.remove()" style="padding: 10px 20px; background: #6B7280; color: white; border: none; border-radius: 6px; cursor: pointer;">Cancel</button>' +
                            '<button onclick="sendMessage()" style="padding: 10px 20px; background: #2563eb; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Send</button>' +
                        '</div>' +
                    '</div>';

                document.body.appendChild(dialog);
            };

            window.sendMessage = function() {
                const message = document.getElementById('message-text').value;
                const selected = Array.from(document.querySelectorAll('.interpreter-checkbox:checked'));
                const phoneNumbers = selected.map(cb => cb.dataset.phone);
                const dialog = document.querySelector('[style*="position: fixed"]');
                const jobId = dialog.getAttribute('data-job-id');

                // Disable send button and show loading state
                const sendButton = event.target;
                sendButton.disabled = true;
                sendButton.textContent = 'Sending...';

                // Send SMS via API
                fetch('/api/send-sms/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        phone_numbers: phoneNumbers,
                        message: message,
                        job_id: jobId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Success!\\n\\nMessages sent: ' + data.sent + '\\nFailed: ' + data.failed);
                        // Close dialog
                        document.querySelector('[style*="position: fixed"]').remove();
                    } else {
                        alert('Error: ' + data.error);
                        sendButton.disabled = false;
                        sendButton.textContent = 'Send';
                    }
                })
                .catch(error => {
                    alert('Error sending messages: ' + error.message);
                    sendButton.disabled = false;
                    sendButton.textContent = 'Send';
                });
            };
        })();
        </script>
        '''

        from django.utils.safestring import mark_safe
        return mark_safe(html)
    available_interpreters_display.short_description = 'Available Interpreters'
