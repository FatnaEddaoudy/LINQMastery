import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Badge } from '@/components/ui/badge';
import type { ProcessingMode } from '@shared/schema';

interface ProcessingModeToggleProps {
  mode: ProcessingMode;
  onModeChange: (mode: ProcessingMode) => void;
  disabled?: boolean;
}

export function ProcessingModeToggle({ mode, onModeChange, disabled }: ProcessingModeToggleProps) {
  return (
    <div className="space-y-3">
      <Label className="text-sm font-medium text-foreground">Processing Mode</Label>
      <RadioGroup
        value={mode}
        onValueChange={(value) => onModeChange(value as ProcessingMode)}
        disabled={disabled}
        className="space-y-3"
      >
        <div className="flex items-center space-x-3">
          <RadioGroupItem value="combined" id="combined" data-testid="radio-combined" />
          <Label
            htmlFor="combined"
            className="flex items-center gap-2 cursor-pointer font-normal"
          >
            Combine into single file
            <Badge variant="secondary" className="text-xs">Recommended</Badge>
          </Label>
        </div>
        <div className="flex items-center space-x-3">
          <RadioGroupItem value="separate" id="separate" data-testid="radio-separate" />
          <Label
            htmlFor="separate"
            className="cursor-pointer font-normal"
          >
            Separate file for each upload
          </Label>
        </div>
      </RadioGroup>
    </div>
  );
}
